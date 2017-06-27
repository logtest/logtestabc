package com.admin;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import org.zeromq.ZMQ;

public class ZmqPubSubscriber {

	
	private String host;
	private String filter;
	
	public ZmqPubSubscriber(String server){
		host = server;
		filter = "";
	}
	

	class ReadInputLoop implements Runnable{
		private String thefilter = "";
		
		public void run(){
			BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
				try {
					while(true){
					thefilter = br.readLine();
				}
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
		}
		
		public String getFilter(){
			return thefilter;
		}
			
	}

	
	public void run(){

		ReadInputLoop readInputLoop = new ReadInputLoop();
		Thread readInputLoopThread = new Thread(readInputLoop);
		readInputLoopThread.start();
		
		ZMQ.Context context = ZMQ.context(1);

		// Socket to talk to server
		System.out.println("Collecting updates from server");
		ZMQ.Socket subscriber = context.socket(ZMQ.SUB);
		subscriber.connect(host);

		//subscriber.subscribe(filter.getBytes());
		subscriber.subscribe("".getBytes()); // subscribe all
		// subscriber.subscribe("Quote".getBytes());	//subscribe Quote only
		
		boolean flag = true;
		while(flag){
			String s = subscriber.recvStr();
			filter = readInputLoop.getFilter();
			if(s.contains(filter)){
				System.out.println(s);
			}
			
		}
		
		subscriber.close();
		context.term();
		
	}
	
	
	public static void main(String[] args) {

		String host;
		
		if(args.length == 0){
			host = "tcp://localhost:5656";
		}else{
			host = args[0];
		}
		
		ZmqPubSubscriber zmqSub = new ZmqPubSubscriber(host);
		zmqSub.run();
		
	}
}