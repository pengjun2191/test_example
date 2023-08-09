import os
import gevent
from test_performance_case.locustfile import WebsiteUser
from locust.env import Environment
from locust.stats import stats_printer, stats_history


def test_locust():
    # setup Environment and Runner
    env = Environment(user_classes=[WebsiteUser])
    env.create_local_runner()

    # start a greenlet that periodically outputs the current stats
    gevent.spawn(stats_printer(env.stats))

    # start a greenlet that save current stats to history
    gevent.spawn(stats_history, env.runner)

    # start the test
    env.runner.start(1, spawn_rate=10)

    # in 60 seconds stop the runner
    gevent.spawn_later(60, lambda: env.runner.quit())

    # wait for the greenlets
    env.runner.greenlet.join()

    env.runner.quit()


def main(args):
    if args.start_type=="master":
        os.system(f"locust  --{args.start_type} -f {args.master_name}")
    else:
        os.system(f"locust  --{args.start_type} -f {args.worker_name}")


if __name__=="__main__":
    from test_performance_case.locust_cli import locust_cli
    args=locust_cli()
    main(args)