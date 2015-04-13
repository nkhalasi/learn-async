import akka.actor.{ActorLogging, Actor}
import concurrent.Future
import concurrent.ExecutionContext.Implicits.global

class BarTender extends Actor with ActorLogging {
    var total = 0
    def receive = {
        case Ticket(quantity) =>
            val s = sender
            total = total + quantity

            log.info(s"I will get $quantity pints for [${s.path}]")

            for (number <- 1 to quantity) {
                log.info(s"Pint $number is coming right up for [${s.path}]")

                //context.system.scheduler.scheduleOnce(1000 milliseconds) {
                //    log.info(s"Pint $number is ready, here you go [${s.path}]")
                //    s ! FullPint(number)
                //}
                
                Future {
                    Thread.sleep(1000)
                    log.info(s"Pint $number is ready, here you go [${s.path}]")
                    s ! FullPint(number)
                }
            }

        case EmptyPint(number) =>
            total match {
                case 1 => 
                    log.info("Ya'all drank those pints quick, time to close up shop")
                    context.system.shutdown()
                case n =>
                    total = total - 1
                    log.info(s"You drank pint $number quick, but there are still $total pints left")
            }
    }
}

