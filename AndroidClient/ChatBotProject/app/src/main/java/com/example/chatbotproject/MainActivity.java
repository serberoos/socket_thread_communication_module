package com.example.chatbotproject;
import android.os.Handler;
import android.os.Message;
import android.os.StrictMode;
import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;


public class MainActivity extends AppCompatActivity {

    Button btn;
    ListView talkContent2;
    EditText clientMsgInput;
    ArrayAdapter<String> adapter;


    private Socket clientSocket;//클라이언트 소켓
    private PrintWriter clientSendMsg; //클라이언트 메세지 송신
    private BufferedReader serverMsg; //서버 메세지 수신
    private int port = 7777; //서버 port
    private final String ip = "192.168.200.121"; // 서버 ip

    private MyHandler myHandler;
    private MyThread myThread;


        protected void onCreate(Bundle savedInstanceState) { //첫 액티비티 열면서 수행할 것들
            super.onCreate(savedInstanceState);
            setContentView(R.layout.activity_main);

            StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
            StrictMode.setThreadPolicy(policy);

            adapter = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1);
            talkContent2 = (ListView)findViewById(R.id.talkContent2);
            talkContent2.setAdapter(adapter);

            try {
                clientSocket = new Socket(ip, port); //클라이언트 소켓 객체 생성
                serverMsg = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
                clientSendMsg = new PrintWriter(clientSocket.getOutputStream(), true);
            } catch (IOException e) {   
                e.printStackTrace();
            }
        //-
            myHandler = new MyHandler();
            myThread = new MyThread();
            myThread.start();


            btn = (Button) findViewById(R.id.sendButton);
            clientMsgInput = (EditText) findViewById(R.id.clientMessageInput);
            btn.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    adapter.add("you : " + clientMsgInput.getText().toString()); //클라이언트 화면에 표시
                    clientSendMsg.println(clientMsgInput.getText().toString()); // 입력된 메세지 보내기
                }
            });
        }


    class MyThread extends Thread {
        @Override
        public void run (){
            while(true) {
                try {
                    //InputStream 값을 읽어와 data에 저장
                    String data = serverMsg.readLine();
                    //Message 객체를 생성, 핸들러에 정보를 보낼 땐 이 메세지 객체를 이용
                    Message msg = myHandler.obtainMessage();
                    msg.obj = data;
                    myHandler.sendMessage(msg);
                }
                catch(Exception e){
                    e.printStackTrace();
                }
            }
        }
    }
    class MyHandler extends Handler { // 메세지 수신 핸들러
        @Override
        public void handleMessage(Message msg) {
            adapter.add("server : " + msg.obj.toString());
        }
    }

}
