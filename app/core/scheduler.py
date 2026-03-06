import schedule


class EventScheduler:

    def __init__(self):
        self.initialized = False

    def setup(self, engine):

        if self.initialized:
            return

        # 1초 시장 tick
        schedule.every(1).seconds.do(engine.market_tick)

        # 5분 세션 체크
        schedule.every(5).minutes.do(engine.session_check)

        # 15분 scanner
        schedule.every(15).minutes.do(engine.scanner_update)

        # 15:10 overnight 평가
        schedule.every().day.at("15:10").do(engine.overnight_eval)

        self.initialized = True

    def run(self):
        schedule.run_pending()
