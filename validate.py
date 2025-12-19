# validator.py
import pandas as pd

def validate_jobs( output_csv="validated_jobs1.csv"):
    input_csv = "timesjobs_Admin_Assistants.csv"
    input_csv1 = "timesjobs_Executive_Assistants.csv"

    df = pd.read_csv(input_csv)
    df1 = pd.read_csv(input_csv1)

    # Combine rows
    final_df = pd.concat([df, df1], ignore_index=True)

    # Job Title,Company,Posted Date,Location,Experience,Salary,Job Description,Skills,Key Details

    # Save all jobs
    final_df.to_csv("All_jobs.csv", index=False)
    print(len(final_df))

    valid_jobs = []
    for _, row in final_df.iterrows():
        desc = row['Job Description'].lower()
        title = row['Job Title'].lower()
        location = row['Location'].lower()

        # Validation rules
        if "remote" in location or "remote" in desc:
            if "english" in desc or "communication" in desc:  # English requirement
                if any(keyword in title for keyword in [
                            "executive  assistant",
                            "admin assistant",
                            "administrative assistant",
                        ]):
                    valid_jobs.append(row)

    df_valid = pd.DataFrame(valid_jobs)
    df_valid = df_valid.drop_duplicates()
    print(len(df_valid))
    df_valid.to_csv(output_csv, index=False)
    return df_valid

if __name__ == "__main__":
    validate_jobs()