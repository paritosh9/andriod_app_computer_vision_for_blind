package com.example.myfirstapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

import android.app.*;
import android.widget.TextView;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;
//import com.chaquo.python.utils.*;

public class MainActivity extends AppCompatActivity{
    TextView textView;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        //setContentView(R.layout.activity_main);

        if(! Python.isStarted())
            Python.start(new AndroidPlatform(this));

        Python py = Python.getInstance();

        PyObject pyf = py.getModule("main");

        PyObject obj = pyf.callAttr("main");


        textView = findViewById(R.id.text);

        //textView.setText(obj.toString());
    }

    // public void run() {
    //    py.getModule("main").callAttr("main");
    //}
}

