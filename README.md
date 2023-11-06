# Sports center with a management and control system for the process of booking and using sports courts

## Roles in the system:

- `Owner` – everything is available;
- `Finance Department` – the sports center card and all settings related to profit calculations are available;
- `Manager` – only the court management card is available (only the manager can approve the booking and transfer);
- `Coach` – a court management card with limited functionality is available (can cancel without intervention
  manager);

### Structure:

1. The fundamental unit is a Sports Center. There is a card of the center, from it there is an opportunity to view the
   number of the working staff, the profitability of employees, as well as monthly/annual profit. Access to
   the management of the sports card of the court is also provided from here. Only people from the finance department
   and the owner have access to the center's card.

2. The following mechanics are implemented in the management of sports courts:
    - `the training step is equal to one hour`;
    - `the center's working hours are from 7 am to 22 pm`;
    - `three types of training are availableк`:
        - `individual`;
        - `split (2 people)`;
        - `group (from three)`;
          (each type of training has its own price. The price consists of a sports court rental fee (depends on the
          season) and a coach fee. The profit is formed from the rental of a sports court and 20% of the coach's fee));
    - `booking for a certain time, postponement of booking, cancellation of booking`;
    - `wholesale time buyback`:
      (Allows you to book a sports court for a long period of time, at least 40 hours of time. Time is not
      it must necessarily go in a row, it can be divided into different days. With a wholesale purchase of 40 hours or
      more, it is provided 15% discount on sports court rental with rounding up to an integer);

3. When logging in from the coach's account, he has only a sports card of the venues available, which
   clearly indicates when, with whom and where the training will take place. The coach has the opportunity to cancel the
   lesson. The trainer sees his theoretical profit depending on his training schedule.
