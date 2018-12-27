from collections import defaultdict
import os 

def build_dict(csv, header = True):
    """
    given a csv file, return a dict, key is filename, dict is label 
    """
    d = dict()
    with open(csv, 'r') as fp:
        for line in fp: 
            if header: 
                header = False
                continue 
            tmp = line.split(',')
            d[tmp[0]] = int(tmp[1])
    return d 


class Eval(object): 
    def __init__(self, public_true_csv, private_true_csv, header = True): 
        self.public_dict = build_dict(public_true_csv, header)
        self.private_dict = build_dict(private_true_csv, header)
        self.public_num = len(self.public_dict) 
        self.private_num = len(self.private_dict)
        self.total = self.public_num + self.private_num
        self.header = header

    def evalulate(self, submission_csv): 
        """
        This eval function depends on each contest. However, inputs and outputs have some forms

        inputs: 
            public_true_csv: path to public_true_csv file 
            private_true_csv: path to private_true_csv file 
            submission_csv: one submission file 
        outputs: 
            public score 
            private score 
        """
        public_count = private_count = 0 
        with open(submission_csv, 'r') as fp: 
            lines = fp.readlines()
            if len(lines) != self.total + +(self.header): 
                # raise an error: number of line incorrect 
                # we need to check other submission errors as well
                # if submission error, the number of submission on that day remains 
                print('submission error')
                return None, None
            flag = self.header
            for line in lines: 
                if flag: 
                    flag = False 
                    continue 
                tmp = line.split(',')
                key = tmp[0]
                lb = int(tmp[1])
                if key in self.public_dict.keys():
                    public_count += +(lb == self.public_dict[key])
                else: 
                    private_count += +(lb == self.private_dict[key])
        return float(public_count)/self.public_num, float(private_count)/self.private_num


class LeaderBoard(object):
    def __init__(self, public_csv, private_csv, reverse = False, header = True):
        """
        if reverse == True, smaller evaluated score ranks higher 
        """
        self.reverse = reverse 
        self.better = max if reverse else min 
        # self.public_lb_all = defaultdict(list)
        self.submissions = defaultdict(int)
        self.public_best = dict()
        # self.private_lb_all = defaultdict(list)
        self.private_best = dict()
        self.eval = Eval(public_csv, private_csv, header)

    def new_submission(self, team, csv_fn):
        print('============================================')
        print('{} submitted {}'.format(team, csv_fn))
        pub_score, pri_score = self.eval.evalulate(os.path.join(team, csv_fn))
        if pub_score == None: # submission error 
            return False 

        self.submissions[team] += 1
        self.public_best[team] = self.better(self.public_best[team], pub_score) \
                if team in self.public_best else pub_score
        ## uncomment the following line if you want to save all scores
        # self.public_lb_all[team].append(pub_score)

        self.private_best[team] = self.better(self.private_best[team], pri_score)\
                if team in self.private_best else pri_score

        ## uncomment the following line if you want to save all scores
        # self.private_lb_all[team].append(pri_score)
         
        return True 

    def display(self, board = 'Public'): 
        tmp = self.public_best if board == 'Public' else self.private_best
        print('{} LeaderBoard'.format(board))
        print('Rank \t team \t score \t #submissions')
        print('---------------------------------------')
        order = sorted(tmp.keys(), key = lambda x:tmp[x], reverse = self.reverse)
        for i, team in enumerate(order):
            print('{} \t {} \t {:.4f} \t {}'.format(i+1, team, tmp[team], 
                self.submissions[team]))
        print('\n')


if __name__ == '__main__':
    lb = LeaderBoard('./public_true.csv', './private_true.csv', reverse = False, header = True)
    lb.new_submission('team1', 'submission1.csv')
    lb.display('Public')
    lb.display('Private')

    lb.new_submission('team2', 'submission3.csv')
    lb.display('Public')
    lb.display('Private')

    lb.new_submission('team3', 'submission5.csv')
    lb.display('Public')
    lb.display('Private')

    lb.new_submission('team1', 'submission2.csv')
    lb.display('Public')
    lb.display('Private')

    lb.new_submission('team2', 'submission4.csv')
    lb.display('Public')
    lb.display('Private')

    lb.new_submission('team3', 'submission6.csv')
    lb.display('Public')
    lb.display('Private')

