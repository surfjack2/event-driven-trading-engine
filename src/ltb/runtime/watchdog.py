import time
import multiprocessing
from ltb.runtime.engine_process import run_engine
from ltb.runtime.workers.market_worker import run_market_worker
from ltb.runtime.workers.strategy_worker import run_strategy_worker
from ltb.runtime.workers.risk_worker import run_risk_worker
from ltb.runtime.workers.analytics_worker import run_analytics_worker
from ltb.runtime.workers.alert_worker import run_alert_worker


def start_process(target, name):
    p = multiprocessing.Process(target=target, name=name)
    p.start()
    return p


def main():

    processes = {}

    processes["engine"] = start_process(run_engine, "engine")
    processes["market"] = start_process(run_market_worker, "market_worker")
    processes["strategy"] = start_process(run_strategy_worker, "strategy_worker")
    processes["risk"] = start_process(run_risk_worker, "risk_worker")
    processes["analytics"] = start_process(run_analytics_worker, "analytics_worker")
    processes["alert"] = start_process(run_alert_worker, "alert_worker")

    while True:

        for name, proc in list(processes.items()):

            if not proc.is_alive():
                print(f"[WATCHDOG] {name} crashed. restarting...")

                if name == "engine":
                    processes[name] = start_process(run_engine, name)

                elif name == "market":
                    processes[name] = start_process(run_market_worker, name)

                elif name == "strategy":
                    processes[name] = start_process(run_strategy_worker, name)

                elif name == "risk":
                    processes[name] = start_process(run_risk_worker, name)

                elif name == "analytics":
                    processes[name] = start_process(run_analytics_worker, name)

                elif name == "alert":
                    processes[name] = start_process(run_alert_worker, name)

        time.sleep(2)


if __name__ == "__main__":
    main()
