class Error_codes():
	def __init__(self):
		self.dt = {
				200 : "HTTP 200 OK",
				400 : "HTTP 400 BAD REQUEST",
				401 : "HTTP 401 UNAUTHORISED",
				403 : "HTTP 403 FORBIDDEN",
				404 : "HTTP 404 PAGE NOT FOUND"
		}
		self.err = {
				"HTTPERR" : 1,
				"URLERR" : 2,
				"INCOMPDL" : 3,
				"NOIMG" : 4
		}

	def error_code_status(self, error_code):
		try:
			status = self.dt[error_code]
		except KeyError:
			status = "Unknown Error"
		return status

	def get_error_list(self):
		return self.err.values()