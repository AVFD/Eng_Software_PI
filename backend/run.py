from app import manager
from app import app


if __name__ == "__main__":
	app.run(debug=True, host='127.0.0.1', port=5000)
	#app.run(debug=True, port=5000)
	#host='192.168.43.128', port=4000, threaded=False
	#manager.run()

	#colocar o ip da VM no campo Host