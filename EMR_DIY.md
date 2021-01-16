## EMR DIY

start ssm session
```
ec2="i-038fb5e2df183ce42" # WUK
aws ssm start-session --target $ec2 --profile=micropole --region=eu-west-1
```

Create your user
```
sudo su - ec2-user
sudo adduser thierryturpin
sudo su - thierryturpin
```

Clone the repository, providing your PAT credentials
```
git clone https://<<your git username>>@github.com/MicropoleBelgium/WUK.git

```

Switch to the `qual` branch
```
git checkout remotes/origin/qual
```

Create your feature branch
```
git checkout -b feature-workshop-thierryturpin
```

Edit the pyspark scripts & verify the GIT status
```
git status
```

example
```
git status
On branch feature-workshop-thierryturpin
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   README.md
```

stage your modified files

commit and push your work (update your username & mail if needed)
```
git commit -m "just a small update of the README"
git push --set-upstream origin feature-workshop-thierryturpin
```

goto: https://github.com/MicropoleBelgium/WUK
open a pull request and describe your work:

```
base repository         base        <--     head repository         compare
thierryturpin/WUK       qual        <--     MicropleBelgium/WUK     <<your feature branch>>
```

![open_pull_request](img/open_pull_request.png)

Submit and EMR step using AWS CLI
...

