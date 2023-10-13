import environ


class EmailMessageComposer():
    def __init__(self):
        self.env = environ.Env()
        environ.Env.read_env()

    def user_reset_message(self, email, users, code):
        subject = "User reset information request for " + email
        message = "Dear User with email " + email + ",\n"
        message += "You are getting this email because you requested either a password reset or username information."
        if users.count() > 1:
            message += "\nIt looks as if you have more than one account with this email.  We will list each account "
            message += "for you."
        for user in users:
            message += "\n\n Your username: " + user.username
            message += "\n To reset password please click on the link " + self.env('BASE_URL')
            message += "accounts/reset?code=" + code + "&user_id=" + str(user.id)

        return {'subject': subject, 'message': message}
