import akka.actor.{ActorLogging, Actor}
import concurrent.Future
import concurrent.ExecutionContext.Implicits.global

class Person extends Actor with ActorLogging {
    def receive = {
        case FullPint(number) =>
            val s = sender
            log.info(s"I will make short work of pint $number")
            Future {
                Thread.sleep(1000)
                log.info(s"Done, here is the empty glass for pint $number")
                s ! EmptyPint(number)
            }
    }
}

