def fuse_scores(gpr_score: float, cv_score: float) -> float:
    # GPR is highly reliable for buried threats; weight it heavier
    gpr_weight = 0.7
    cv_weight = 0.3
    fused = (gpr_score * gpr_weight) + (cv_score * cv_weight)
    return round(fused, 2)

def classify(fused_score: float, threshold: float = 0.65) -> str:
    if fused_score >= threshold:
        return "THREAT"
    return "CLEAR"