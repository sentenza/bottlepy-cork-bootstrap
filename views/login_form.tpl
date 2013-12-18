<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="shortcut icon" href="../../docs-assets/ico/favicon.png">

    <title>Signin Template</title>

    <!-- Bootstrap core CSS -->
    <link href="assets/css/bootstrap.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="assets/css/signin.css" rel="stylesheet">

    <!-- Just for debugging purposes. Don't actually copy this line! -->
    <!--[if lt IE 9]><script src="../../docs-assets/js/ie8-responsive-file-warning.js"></script><![endif]-->

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
<script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
<script src="https://oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
<![endif]-->
  </head>

  <body>

    <div class="container">
      <form class="form-signin" role="form" action="login" method="post" name="login">
        <h2 class="form-signin-heading">Please sign in</h2>
        <input type="text" class="form-control" name="username" placeholder="Username" required autofocus>
        <input type="password" class="form-control" name="password" placeholder="Password" required>
        <label class="checkbox">
          <input type="checkbox" value="remember-me"> Remember me
        </label>
        <button class="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>
      </form>


      <form class="form-signin" role="form" action="register" method="post" name="signup">
        <h2 class="form-signin-heading">Please sign up</h2>
        <input type="text" class="form-control" name="username" placeholder="Username" required autofocus>
        <input type="text" class="form-control" name="email_address" placeholder="Email address" required>
        <input type="password" class="form-control" name="password" placeholder="Password" required>
        <button class="btn btn-lg btn-primary btn-block" type="submit">Sign up</button>
      </form>

      <form class="form-signin" role="form" action="reset_password" method="post" name="password_reset">
        <h2 class="form-signin-heading">Password reset</h2>
        <input type="text" class="form-control" name="username" placeholder="Username" required autofocus>
        <input type="text" class="form-control" name="email_address" placeholder="Email address" required>
        <button class="btn btn-lg btn-primary btn-block" type="submit">Send request</button>
      </form>


    </div> <!-- /container -->


    <!-- Bootstrap core JavaScript
================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
  </body>
</html>


