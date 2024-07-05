package com.example.notebook;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

public class RegisterActivity extends AppCompatActivity {

    private EditText et_username;
    private EditText et_password;
    private SharedPreferences sharedPreferences;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        //初始化SharedPreferences
        final SharedPreferences SharedPreferences = getSharedPreferences("user", MODE_PRIVATE);

        //初始化控件
        et_username =findViewById(R.id.et_username);
        et_password =findViewById(R.id.et_password);


        //返回
        findViewById(R.id.toolbar).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                finish();
            }
        });

        //点击注册
        findViewById(R.id.register).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String username = et_username.getText().toString();
                String password = et_password.getText().toString();

                if (TextUtils.isEmpty(username) && TextUtils.isEmpty(password)) {
                    Toast.makeText(RegisterActivity.this, "请输入用户名和密码", Toast.LENGTH_SHORT).show();
                }else {
                    //注册成功

                    SharedPreferences.Editor edit = SharedPreferences.edit();
                    edit.putString("username"+username,username);
                    edit.putString("password"+username,password);
                    //提交
                    edit.commit();
                    Toast.makeText(RegisterActivity.this, "注册成功，请登入", Toast.LENGTH_SHORT).show();
                    finish();
                }
            }
        });
    }
}