import logging
import time
from xudd.actor import Actor
from xudd.hive import Hive

_log = logging.getLogger(__name__)

class DiningTable(Actor):
    def __init__(self, hive, id):
        super().__init__(hive, id)
        self.message_routing.update(
            {'layout_philosophers_and_forks': self.setup_table}
        )

    def _forks(self):
        f1 = self.hive.create_actor(Fork, name='Fork 1')
        f2 = self.hive.create_actor(Fork, name='Fork 2')
        f3 = self.hive.create_actor(Fork, name='Fork 3')
        f4 = self.hive.create_actor(Fork, name='Fork 4')
        f5 = self.hive.create_actor(Fork, name='Fork 5')
        return f1, f2, f3, f4, f5

    def _philosophers(self):
        f1, f2, f3, f4, f5 = self._forks()
        _log.info('All forks: {0}'.format((f1, f2, f3, f4, f5)))

        p1 = self.hive.create_actor(Philosopher, name='P1', think_time=2, eat_time=2, forks=(f1, f2))
        p2 = self.hive.create_actor(Philosopher, name='P2', think_time=5, eat_time=3, forks=(f2, f3))
        p3 = self.hive.create_actor(Philosopher, name='P3', think_time=7, eat_time=2, forks=(f3, f4))
        p4 = self.hive.create_actor(Philosopher, name='P4', think_time=4, eat_time=3, forks=(f4, f5))
        p5 = self.hive.create_actor(Philosopher, name='P5', think_time=3, eat_time=4, forks=(f5, f1))
        return p1, p2, p3, p4, p5

    def setup_table(self, message):
        ps = self._philosophers()
        _log.info('Finished setting up the dining table')
        for p in ps:
            self.hive.send_message(to=p, directive='think_and_eat')
        _log.info('Instructed all philosophers to start thinking')

class Philosopher(Actor):
    def __init__(self, hive, id, name, think_time, eat_time, forks):
        super().__init__(hive, id)
        self.name = name
        self.think_time = think_time
        self.eat_time = eat_time
        self.left_fork, self.right_fork = forks

        self.message_routing.update(
            {"think_and_eat": self.think_and_eat}
        )
    
    def _think(self):
        _log.info('{id}: I am thinking for {time} seconds'.format(id=self.id, time=self.think_time))
        time.sleep(self.think_time)
        _log.info('{id}: I am done thinking'.format(id=self.id))

    def _eat(self):
        _log.info('{id}: I am EATING. I will need {time} seconds'.format(id=self.id, time=self.eat_time))
        time.sleep(self.eat_time)
        _log.info('{id}: I am done EATING'.format(id=self.id))

    def think_and_eat(self, message):
        while True:
            lf_status = yield self.wait_on_message(to=self.left_fork, directive='status')
            rf_status = yield self.wait_on_message(to=self.right_fork, directive='status')
            _log.info('P[{pid}] has {fs}'.format(pid=self.id, fs=(lf_status.body, rf_status.body)))
            self._think()
            lf_resp = yield self.wait_on_message(to=self.left_fork, directive='take')
            rf_resp = yield self.wait_on_message(to=self.right_fork, directive='take')
            _log.info('P[{pid}] now has {fs}'.format(pid=self.id, fs=(lf_resp.body, rf_resp.body)))
            rejected_statuses = [True if r.body['status'] == 'Rejected' else False for r in (lf_resp, rf_resp)]
            _log.info('{id}: {statuses}'.format(id=self.id, statuses=rejected_statuses))
            if any(rejected_statuses):
                _log.info('{id}: Did not find both forks...will go back to thinking.'.format(id=self.id))
                accepted = [r for r in (lf_resp, rf_resp) if r.body['status'] == 'Accepted']
                for r in accepted:
                    self.hive.send_message(to=r.body['id'], directive='finished')
            else:
                _log.info('{id}: Got both forks...now eating.'.format(id=self.id))
                self._eat()
                self.hive.send_message(to=self.left_fork, directive='finished')
                self.hive.send_message(to=self.right_fork, directive='finished')
                _log.info('{id}: Finished eating. Going back to thinking.'.format(id=self.id))


class Fork(Actor):
    def __init__(self, hive, id, name):
        super().__init__(hive, id)
        self.name = name
        self.available = True
        self.message_routing.update(
            {'take': self.take_request, 'finished': self.finished, 'status': self.status}
        )

    def take_request(self, message):
        _log.info('{p} is attempting to take F[{id}] which is currently {status}'.format(p=message.from_id, id=self.id, status='Available' if self.available else 'Unavailable'))
        if self.available:
            self.available = False
            message.reply(body={'status': 'Accepted', 'id': self.id})
        else:
            message.reply(body={'status': 'Rejected', 'id': self.id})

    def finished(self, message):
        assert(self.available == False)
        self.available = True

    def status(self, message):
        message.reply(body={'status': 'Available' if self.available else 'Unavailable', 'id': self.id})


def main():
    logging.basicConfig(level=logging.INFO)
    hive = Hive()
    hive.create_actor(DiningTable, id="diningtable")
    hive.send_message(to="diningtable", directive="layout_philosophers_and_forks")
    hive.run()

if __name__ == "__main__":
    main()
