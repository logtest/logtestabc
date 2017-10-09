
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


period:15;

m:select first open, max high, min low,last close by sym, (period*60000000000) xbar time from minutely;
update macd:MACD[close;12;26;9] by sym from `sym`time xasc `m;

prepareData:{ [data;symbol;signal1;refdata;symbolref;signal2]
 test:? [data;enlist(=;`sym;enlist symbol);0b;`sym`time`open`close`signal1!`sym`time`open`close,signal1];
 if[0<count refdata; test: test lj 1!?[refdata;enlist(=;`sym;enlist symbolref);0b;`time`signal2!`time,signal2] ];
 test
}

test:prepareData[`m;`B;`macd;`m;`F;`macd];
update opennxt: next open, closenxt:next close, sig:{$[(x>=0)&y<0;1i;(x<0)&y>0;-1i;0 ]}'[signal2;prev signal2] by sym from `test
test

select n:count i, avg rtn by sig from update rtn:RTNBPS[opennxt;next opennxt] by sym from select from test where sig <>0



