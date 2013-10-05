from web.forms import AuthForm
def printAuthForm(request):
	return{
		'auth_form': AuthForm()
	}
