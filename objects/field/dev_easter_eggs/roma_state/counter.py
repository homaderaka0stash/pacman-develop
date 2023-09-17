class Counter:
    def __init__(self, final_res):
        self.final_res = final_res
        self.cnt = 0

    def cnt_upgrade(self):
        self.cnt += 1

    def check_cnt(self):
        if self.cnt >= self.final_res:
            return True
        else:
            return False
