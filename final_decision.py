def final_decision(clip_result, artifact_score, artifact_reasons):
    score = 0
    reasons = []

    if clip_result["ai_generated"]:
        score += 2
        reasons.extend(clip_result["reasons"])

    score += artifact_score
    reasons.extend(artifact_reasons)

    if score >= 3:
        return {
            "ai_generated": True,
            "confidence": min(95, 60 + score * 10),
            "reasons": list(set(reasons))
        }
    else:
        return {
            "ai_generated": False,
            "confidence": min(95, 60 + (3 - score) * 10),
            "reasons": list(set(reasons))
        }
