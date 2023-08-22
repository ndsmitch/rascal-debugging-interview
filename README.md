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
