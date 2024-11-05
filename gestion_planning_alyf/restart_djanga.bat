
@echo off 
:loop
echo Restarting Django runserver...
python C:\Users\alyf\projet-stage-Alyf-Django\demo_alyf\ waitress-serve --host:0.0.0.0 --port=80 demo_alyf.wsgi:application
goto loop