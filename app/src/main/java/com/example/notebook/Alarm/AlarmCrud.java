package com.example.notebook.Alarm;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

import java.util.ArrayList;
import java.util.List;

public class AlarmCrud {
    SQLiteOpenHelper dbHandler;
    SQLiteDatabase db;
    private static final String[] columns = {
            PlanDatabase.ID,
            PlanDatabase.TITLE,
            PlanDatabase.CONTENT,
            PlanDatabase.TIME,
            PlanDatabase.USER
    };

    public AlarmCrud(Context context){
        dbHandler = new PlanDatabase(context);
    }

    public void open(){
        db = dbHandler.getWritableDatabase();
    }

    public void close(){
        dbHandler.close();
    }

    public Plan addPlan(Plan plan){
        // add a plan object to database
        ContentValues contentValues = new ContentValues();
        contentValues.put(PlanDatabase.TITLE, plan.getTitle());
        contentValues.put(PlanDatabase.CONTENT, plan.getContent());
        contentValues.put(PlanDatabase.TIME, plan.getTime());
        contentValues.put(PlanDatabase.USER, plan.getUser());
        long insertId = db.insert(PlanDatabase.TABLE_NAME, null, contentValues);
        plan.setId(insertId);
        return plan;
    }
    //应有查询功能，但要新增界面，暂时还没想好
    public Plan getPlan(long id){
        // get a plan from database using cursor index
        Cursor cursor = db.query(PlanDatabase.TABLE_NAME, columns, PlanDatabase.ID + "=?",
                new String[]{String.valueOf(id)}, null, null, null, null);
        if (cursor != null) cursor.moveToFirst();
        Plan e = new Plan(cursor.getString(cursor.getColumnIndex(PlanDatabase.TITLE)),
                cursor.getString(cursor.getColumnIndex(PlanDatabase.CONTENT)),
                cursor.getString(cursor.getColumnIndex(PlanDatabase.TIME)),
                cursor.getString(cursor.getColumnIndex(PlanDatabase.USER)));
        e.setId(cursor.getLong(cursor.getColumnIndex(PlanDatabase.ID)));
        return e;
    }

    public List<Plan> getAllPlans(String user){
        Cursor cursor = db.query(PlanDatabase.TABLE_NAME, columns, PlanDatabase.USER + "=?",
                new String[]{user}, null, null, null);

        List<Plan> plans = new ArrayList<>();
        if (cursor.getCount() > 0) {
            while (cursor.moveToNext()) {
                Plan plan = new Plan();
                plan.setId(cursor.getLong(cursor.getColumnIndex(PlanDatabase.ID)));
                plan.setTitle(cursor.getString(cursor.getColumnIndex(PlanDatabase.TITLE)));
                plan.setContent(cursor.getString(cursor.getColumnIndex(PlanDatabase.CONTENT)));
                plan.setTime(cursor.getString(cursor.getColumnIndex(PlanDatabase.TIME)));
                plan.setUser(cursor.getString(cursor.getColumnIndex(PlanDatabase.USER)));
                plans.add(plan);
            }
        }
        return plans;
    }

    public int updatePlan(Plan plan) {
        // update the info of an existing plan
        ContentValues values = new ContentValues();
        values.put(PlanDatabase.TITLE, plan.getTitle());
        values.put(PlanDatabase.CONTENT, plan.getContent());
        values.put(PlanDatabase.TIME, plan.getTime());
        values.put(PlanDatabase.USER, plan.getUser());
        // updating row
        return db.update(PlanDatabase.TABLE_NAME, values,
                PlanDatabase.ID + "=?", new String[]{String.valueOf(plan.getId())});
    }

    public void removePlan(Plan plan) {
        // remove a plan according to ID value
        db.delete(PlanDatabase.TABLE_NAME, PlanDatabase.ID + "=" + plan.getId(), null);
    }
}