import akka.actor.{ActorSystem, Props}
import akka.actor.{ActorLogging, Actor, ActorRef}
import akka.pattern.ask
import akka.util.Timeout
import concurrent.{Await, Future}
import concurrent.duration._
import concurrent.ExecutionContext.Implicits.global

case object Take
case object Finished

class TakeRequestStatus()
case object Accepted extends TakeRequestStatus
case object Rejected extends TakeRequestStatus

case object Think
case object Eat

class Fork extends Actor with ActorLogging {
    var available = true
    def receive = {
        case Take =>
            if (available) {
                available = false
                sender ! Accepted
            } else {
                sender ! Rejected
            }
        case Finished => available = true
    }
}

class Philosopher(val leftFork:ActorRef, val rightFork:ActorRef, private var appetite: Int) extends Actor with ActorLogging {
    implicit val timeout = Timeout(5 seconds)
    def receive = {
        case Think => 
            log.info(s"I am thinking")
            Future {
                Thread.sleep(1000)
                val f1 = leftFork ? Take
                val f2 = rightFork ? Take

                val r1 = Await.result(f1, timeout.duration).asInstanceOf[TakeRequestStatus]
                val r2 = Await.result(f2, timeout.duration).asInstanceOf[TakeRequestStatus]
            
                (r1, r2) match {
                    case (Accepted, Accepted) => self ! Eat
                    case (Accepted, Rejected) => leftFork ! Finished
                    case (Rejected, Accepted) => rightFork ! Finished
                    case (Rejected, Rejected) => self ! Think
                }
            }
        case Eat => 
            log.info(s"I am eating")
            Future {
                Thread.sleep(1000)
                leftFork ! Finished
                rightFork ! Finished
                self ! Think
            }
    }
}


object DiningPhilosopher extends App {
    val system = ActorSystem("dining-philosopher")

    val f1 = system.actorOf(Props(new Fork), "F1")
    val f2 = system.actorOf(Props(new Fork), "F2")
    val f3 = system.actorOf(Props(new Fork), "F3")
    val f4 = system.actorOf(Props(new Fork), "F4")
    val f5 = system.actorOf(Props(new Fork), "F5")

    val p1 = system.actorOf(Props(new Philosopher(f1, f2, 3)), "P1")
    val p2 = system.actorOf(Props(new Philosopher(f2, f3, 3)), "P2")
    val p3 = system.actorOf(Props(new Philosopher(f3, f4, 3)), "P3")
    val p4 = system.actorOf(Props(new Philosopher(f4, f5, 3)), "P4")
    val p5 = system.actorOf(Props(new Philosopher(f5, f1, 3)), "P5")
    for (p <- List(p1, p2, p3, p4, p5)) {
        p ! Think
    }
    println("All philosophers have been instructed to start their thinking and eating cycles")

    system.awaitTermination()
}
