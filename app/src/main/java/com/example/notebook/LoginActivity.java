package com.example.notebook;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.View;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

public class LoginActivity extends AppCompatActivity {

    private EditText et_username;
    private EditText et_password;
    private SharedPreferences sharedPreferences;
    private CheckBox checkbox;
    private boolean is_login;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);


        //初始化SharedPreferences
        final SharedPreferences SharedPreferences = getSharedPreferences("user", MODE_PRIVATE);

        //是否勾选了记住密码
        is_login = SharedPreferences.getBoolean("is_login",false);

        //初始化控件
        et_username =findViewById(R.id.et_username);
        et_password =findViewById(R.id.et_password);
        checkbox =findViewById(R.id.checkbox);
       /* if (is_login){
            String username = SharedPreferences.getString("username","");
            String password = SharedPreferences.getString("password","");
            et_username.setText(username);
            et_password.setText(password);
            checkbox.setChecked(true);
        }*/
        //点击注册
        findViewById(R.id.register).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //跳转到注册页面
                Intent intent = new Intent(LoginActivity.this,RegisterActivity.class);
                startActivity(intent);
            }
        });

        findViewById(R.id.forgot).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(LoginActivity.this, ForgetPasswordActivity.class));
            }
        });

        //登录
        findViewById(R.id.login).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String username = et_username.getText().toString();
                String password = et_password.getText().toString();

                if (TextUtils.isEmpty(username) && TextUtils.isEmpty(password)) {
                    Toast.makeText(LoginActivity.this, "请输入用户名和密码", Toast.LENGTH_SHORT).show();
                }else {
                    String name = SharedPreferences.getString("username"+username,null);
                    String pwd = SharedPreferences.getString("password"+username,null);
                    if (username.equals(name) && password.equals(pwd)){

                        SharedPreferences.Editor edit = SharedPreferences.edit();
                        edit.putBoolean("is_login",is_login);
                        edit.putString("username",username);
                        edit.putString("password",password);
                        edit.commit();

                        MainActivity.user = username;
                        //登入成功,跳转主页面
                        Intent intent =new Intent(LoginActivity.this,MainActivity.class).putExtra("name",username);
                        startActivity(intent);
                        finish();
                    }else {
                        Toast.makeText(LoginActivity.this, "用户名或密码错误", Toast.LENGTH_SHORT).show();
                    }
                }

            }
        });

        //checkbox
        checkbox.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton compoundButton, boolean isChecked) {
                is_login =isChecked;
            }
        });

    }
}