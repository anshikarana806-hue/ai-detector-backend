def final_decision(image_result=None, video_result=None):
    if image_result:
        return image_result
    if video_result:
        return video_result
    return {"error": "No media provided"}
