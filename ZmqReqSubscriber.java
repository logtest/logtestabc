
import java.util.Scanner;

import org.zeromq.ZMQ;

public class ZmqReqSubscriber {

	public static void main(String[] args) {

		String host;
		
		if(args.length == 0){
			host = "tcp://localhost:5978";
		}else{
			host = args[0];
		}
		ZMQ.Context context = ZMQ.context(1);
		Scanner reader = new Scanner(System.in);

		// Socket to talk to server
		System.out.println("Collecting updates from server");
		ZMQ.Socket subscriber = context.socket(ZMQ.REQ);
		subscriber.connect(host);


		boolean flag = true;
		while(flag){
			System.out.print("Admin->");
			String request = reader.nextLine();
			if(request.toLowerCase().compareTo("exit") == 0 || request.toLowerCase().compareTo("quit") == 0){
				flag = false;
			}else{
				subscriber.send(request.getBytes(), 0);
				byte[] reply = subscriber.recv(0);
				System.out.println(new String(reply));
				
			}
		}
		subscriber.close();
		context.term();
	}
}