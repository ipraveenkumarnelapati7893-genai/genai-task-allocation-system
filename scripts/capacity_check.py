import pandas as pd

tasks = pd.read_csv("../data/tasks.csv")
vendors = pd.read_csv("../data/vendors.csv")

results = []

for _, task in tasks.iterrows():

    matching_vendor = vendors[
        vendors["Language"] == task["Language"]
    ]

    if not matching_vendor.empty:

        vendor = matching_vendor.iloc[0]

        estimated_days = (
            task["Volume"] /
            vendor["Daily_Capacity"]
        )

        risk = "LOW"

        if estimated_days > task["SLA_Days"]:
            risk = "HIGH"

        utilization = round(
            (
                task["Volume"] /
                (
                    vendor["Daily_Capacity"]
                    * task["SLA_Days"]
                )
            ) * 100,
            2
        )

        results.append({
            "Task_Name": task["Task_Name"],
            "Priority": task["Priority"],
            "Language": task["Language"],
            "Vendor": vendor["Vendor"],
            "Estimated_Days": round(estimated_days, 2),
            "SLA_Days": task["SLA_Days"],
            "Utilization_Percentage": utilization,
            "Risk": risk
        })

output = pd.DataFrame(results)

print("\n===== GENAI OPERATIONS FORECAST =====\n")
print(output)

output.to_csv(
    "../outputs/forecast_report.csv",
    index=False
)

print("\nForecast report exported successfully.")