package com.example.notebook;

public class Note {
    private long id;
    private String content;
    private String time;
    private int tag;
    private String user;

    public String getUser() {
        return user;
    }
    public void setUser(String user) {
        this.user = user;
    }

    public Note() {
    }

    public Note(String content, String time, int tag,String user) {
        this.content = content;
        this.time = time;
        this.tag = tag;
        this.user = user;
    }
    public long getId() {
        return id;
    }

    //返回笔记的内容
    public String getContent() {
        return content;
    }

    public String getTime() {
        return time;
    }

    public void setId(long id) {
        this.id = id;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public void setTime(String time) {
        this.time = time;
    }


    public int getTag() {
        return tag;
    }

    public void setTag(int tag) {
        this.tag = tag;
    }

    @Override
    public String toString() {
        return content + "\n" + time.substring(5,16) + " "+ id;
    }
}
