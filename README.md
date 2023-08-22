# Flying the Rascal

You are maintaining the systems that control your world's most advanced star cruiser, The Rascal.
To maintain control of the ship all commands must be given to the Isopalavial Interface.
The Isopalavial Interface controls the Firomactal Drive and the Ramistat Core.
The Ramistat Core must keep the Ontarian Manifold at 40000KRGs for The Rascal to fly.

Mission control will not let The Rascal take off until all malfunctioning tests have been diagnosed.
Your job is to take a look through the test results, application logs, and code to determine the cause of the failed tests.
Recommendations for solving the errors are appreciated.

# System Diagram

```
   🧠    - You
   |
   🖥️    - Isopalavial Interface
   /\
  /  🚂  - Firomactal Drive
 /  /
🧊 /     - Ramistat Core
| /
🔥       - Ontarian Manifold
```

# Interview Instructions

The AI previously managing the ship went haywire and rewrote the git history in the rascal systems.
Instead of a pristine and useful git log you now have one commit "bork bork bork" which is broken.
1. Take a look at `pytest.log` to determine the test failures.
2. Determine the relevant file in the `logs` folder to evaluate the root cause.
3. Analyze the source code for relevant errors.
4. Look up unknown solutions on the internet - stack overflow, mozilla, and relevant api documentation will be helpful.
There is no need to commit changes or write code at all - solutions will be discussed verbally.

# Solutions

To confirm your solutions, feel free to check out the alternative branches in the repository.

# Run it Yourself

Requires Python 3.8 specifically. Should you wish to run the program yourself, run the following commands.

```bash
source neuralink.sh
./test.sh
```

Shutdown when you're done
```bash
./shutdown.sh
```
