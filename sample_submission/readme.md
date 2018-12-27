
Để đánh giá điểm của các bài nộp, mỗi cuộc thi cần ít nhất ba files: 

1. `public_true.csv` chứa ground truth của tập public test. 

2. `private_true.csv` chứa ground truth của tập private test. 

3. `leaderboad.py` để cập nhật leaderboard mỗi khi có submission mới. :w

```
lb = LeaderBoard('./public_true.csv', './private_true.csv', reverse = True, header = True)
lb.new_submission(team, submission_csv)
lb.display('Public')
lb.display('Private')
```
với `submission_csv` là file do đội `team` nộp.

Các file này admin cần cung cấp ngay khi tạo cuộc thi. 
