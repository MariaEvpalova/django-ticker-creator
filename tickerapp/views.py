from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from moviepy.editor import TextClip, CompositeVideoClip
import os
from .models import Request

@csrf_exempt
def create_video(request):
    try:
        text = request.GET.get('text', 'Running Text')
        output_file = 'running_text.mp4'

        # Capture the IP address and user agent
        ip_address = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT')

        # Save the request to the database with additional information
        Request.objects.create(text=text, ip_address=ip_address, user_agent=user_agent)

        # Set ImageMagick path
        if os.path.exists('/usr/bin/convert'):
            os.environ['IMAGEMAGICK_BINARY'] = '/usr/bin/convert'
        elif os.path.exists('/usr/local/bin/convert'):
            os.environ['IMAGEMAGICK_BINARY'] = '/usr/local/bin/convert'

        # Create the text clip
        text_clip = TextClip(text, fontsize=72, color='white')
        text_width = text_clip.w

        # Define the animation function for moving text
        def moving_text(t):
            return (100 - (100 + text_width) * t / 3, 'center')

        text_clip = text_clip.set_position(moving_text).set_duration(3)
        video = CompositeVideoClip([text_clip], size=(100, 100)).set_duration(3)
        video.write_videofile(output_file, fps=24)

        # Return the video file as a response
        with open(output_file, 'rb') as f:
            video_data = f.read()

        response = HttpResponse(video_data, content_type='video/mp4')
        response['Content-Disposition'] = f'attachment; filename="{output_file}"'
        return response
    except Exception as e:
        return HttpResponse(f"Error creating video: {e}", status=500)
