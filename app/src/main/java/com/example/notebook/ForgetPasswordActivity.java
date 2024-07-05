package com.example.notebook;


import android.content.SharedPreferences;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

public class ForgetPasswordActivity extends AppCompatActivity{
        private EditText et_forget_username;
        private EditText et_new_password;
        private SharedPreferences sharedPreferences;

        @Override
        protected void onCreate(Bundle savedInstanceState) {
            super.onCreate(savedInstanceState);
            setContentView(R.layout.activity_forgot_password);

            //初始化SharedPreferences
            sharedPreferences = getSharedPreferences("user", MODE_PRIVATE);

            //初始化控件
            et_forget_username = findViewById(R.id.et_forget_username);
            et_new_password = findViewById(R.id.et_new_password);

            //返回
            findViewById(R.id.toolbar).setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    finish();
                }
            });


            //点击忘记密码
            findViewById(R.id.forget_password).setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    String forgetUsername = et_forget_username.getText().toString();
                    String newPassword = et_new_password.getText().toString();

                    if (TextUtils.isEmpty(forgetUsername) || TextUtils.isEmpty(newPassword)) {
                        Toast.makeText(ForgetPasswordActivity.this, "请输入用户名和新密码", Toast.LENGTH_SHORT).show();
                    } else {
                        //更新密码
                        if (sharedPreferences.contains("username" + forgetUsername)) {
                            SharedPreferences.Editor edit = sharedPreferences.edit();
                            edit.putString("password" + forgetUsername, newPassword);
                            //提交
                            edit.commit();
                            Toast.makeText(ForgetPasswordActivity.this, "密码更新成功，请登录", Toast.LENGTH_SHORT).show();
                            finish();
                        } else {
                            Toast.makeText(ForgetPasswordActivity.this, "用户名不存在", Toast.LENGTH_SHORT).show();
                        }
                    }
                }
            });
        }

}
