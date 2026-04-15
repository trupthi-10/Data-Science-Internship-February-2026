from chains.pipeline import run_pipeline

if __name__ == "__main__":
    resume = open("sample_data/strong_resume.txt").read()
    jd = open("sample_data/job_description.txt").read()

    result = run_pipeline(resume, jd)
    print(result)
