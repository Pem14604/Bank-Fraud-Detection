# Use Case: To detect the fraud transaction in the bank

In this model we are taking four parameters into consideration to detect anomaly, raise alert and legit the transaction.

## Parameter’s Detail:
- City of Transaction
- Total Number Of Transaction In That City
- Withdrawal Amount
- Last Date Of Transaction



**Based on these parameters we are calculating Mean, Variance, Z-Score and Interquartile Range.**

**Comparing above calculated values with the threshold values calculated from the user past behavior to decide the anomaly, alert and legit.**
