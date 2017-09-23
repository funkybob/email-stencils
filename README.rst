email-stencils
==============

Produce emails using Stencil templates.

Quick Start
-----------

1. Create a ``stencil.TemplateLoader``

   .. code-block:: python

      import stencil

      loader = stencil.TemplateLoader(['./templates/'])

2. Write a template

   .. code-block:: html

	{% block Subject %} Welcome to Nifty Service (TM) {% endblock %}
	{% block body %}
	Welcome!

	We're so happy you signed up to use Nifty Service (TM)!

	Please click here to activate your account: http://{{ activation_link }}

	{% endblock %}
	{% block html %}
	<h1>Welcome!</h2>

	<p>We're so happy you signed up to use Nifty Service &trade;!</p>

	Please click <a href="https://{{ activation_link }}">here</a> to activate your account!
	{% endblock %}

3. Generate the message

   .. code-block:: python

      import email_stencil
      msg = email_stencil.build_message('email/welcome.email', {'activation_link': 'nifty.service/account/activate/'}, loader, ...)

4. Send the message!

   .. code-block:: python

      import smtplib

      s = smtplib.SMTP('localhost')
      s.send_message(msg)
      s.quit()


