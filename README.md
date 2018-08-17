# Appointment Scheduling Algorithm

## Task
Find minimum number of hotel rooms need to be prepared for input list of booking time intervals. One booking reserves exact one room and one room hosts exact one booking at a time.

## Solution algorithm
Sort the booking intervals by start datetime and appoint them one by one to the first room that they can go into. This will be optimal because in order to require a new room `k` when appointing, it must be the case that `k - 1` rooms were occupied at the start datetime of the interval being appointed, so at least `k` intervals overlap at that time so they couldn't have been given fewer than `k` rooms anyway.
