from chains.skill_extraction import extract_skills
from chains.matching import match_skills
from chains.scoring import score_candidate
from chains.explanation import generate_explanation

def run_pipeline(resume, jd):
    skills = extract_skills(resume)
    match = match_skills(skills, jd)
    score = score_candidate(match)
    explanation = generate_explanation(score, match)

    return {
        "skills": skills,
        "match": match,
        "score": score,
        "explanation": explanation
    }
