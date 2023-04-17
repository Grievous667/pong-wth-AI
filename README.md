# pong-wth-AI
Classic pong with a few twists. Made in Pygame.

This mess of code is something I created for Python practice. To play, dowload to a unique folder and run the py file via python.

Known issues:
1. The 'statistics' screen has not been implemented yet. Who knows if I'll ever get around to it.
2. The buttons labeled 'advanced settings' and 'presets' have not had their functionality implemented yet. ibid.
3. At extremely high ball speeds (achievable only through the 'constant acceleration option), the ball can phase through the paddles because it increments itself a distance greater than the paddle width in one frame. This issue is also present if the fps is lowered.
4. The AI can very occasionally trap the ball between the paddle and the arena border. Just quit and start a new game.
