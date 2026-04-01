def generate_feedback(visual_score, audio_metrics, transcript):
    """
    Generates behavioral feedback based on multimodal inputs.
    """
    feedback_points = []
    performance_score = 0

    # 1. Visual Integrity
    if visual_score > 0.8:
        feedback_points.append("✅ Excellent eye contact and presence.")
        performance_score += 3
    elif visual_score > 0.5:
        feedback_points.append("⚠️ Good, but try to minimize looking away from the camera.")
        performance_score += 1
    else:
        feedback_points.append("❌ Eye contact was poor. Focus on the camera to show confidence.")

    # 2. Vocal Energy
    energy = audio_metrics.get("energy", 0)
    if energy > 0.05:
        feedback_points.append("✅ Your voice was clear and authoritative.")
        performance_score += 3
    elif energy < 0.01:
        feedback_points.append("❌ You were too quiet. Speak with more energy.")
    else:
        feedback_points.append("⚠️ Voice energy was moderate. Could be more expressive.")
        performance_score += 1

    # 3. Substance
    words = len(transcript.split())
    if words > 40:
        feedback_points.append("✅ Very detailed explanation.")
        performance_score += 4
    elif words > 15:
        feedback_points.append("⚠️ Reasonable detail, but could be expanded.")
        performance_score += 2
    else:
        feedback_points.append("❌ Answer was too brief. Use the STAR method.")

    return feedback_points, performance_score