def score_candidate(match):
    try:
        score = int(''.join(filter(str.isdigit, match)))
        return min(score, 100)
    except:
        return 50
