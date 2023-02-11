package com.bcore.poc;

public class GetInfo {

    
    private String LocalAddr;
    private String LocalName;
    private int LocalPort;
    
    private String RemoteAddr;
    private String RemoteName;
    private int RemotePort;


    private String ServerName;
    private int ServerPort;

    private String Date;


    public String getLocalAddr() {
        return LocalAddr;
    }
    public String getServerName() {
        return ServerName;
    }
    public void setServerName(String serverName) {
        this.ServerName = serverName;
    }
    public int getServerPort() {
        return ServerPort;
    }
    public void setServerPort(int serverPort) {
        this.ServerPort = serverPort;
    }
    public String getDate() {
        return Date;
    }
    public void setDate(String date) {
        this.Date = date;
    }
    public int getRemotePort() {
        return RemotePort;
    }
    public void setRemotePort(int remotePort) {
        this.RemotePort = remotePort;
    }
    public String getRemoteName() {
        return RemoteName;
    }
    public void setRemoteName(String remoteName) {
        this.RemoteName = remoteName;
    }
    public String getRemoteAddr() {
        return RemoteAddr;
    }
    public void setRemoteAddr(String remoteAddr) {
        this.RemoteAddr = remoteAddr;
    }
    public int getLocalPort() {
        return LocalPort;
    }
    public void setLocalPort( int localPort) {
        this.LocalPort = localPort;
    }
    public String getLocalName() {
        return LocalName;
    }
    public void setLocalName(String localName) {
        this.LocalName = localName;
    }
    public void setLocalAddr(String localAddr) {
        this.LocalAddr = localAddr;
    }
    @Override
    public String toString() {
        return "{Date:" + Date + ", LocalAddr:" + LocalAddr + ", LocalName:" + LocalName + ", LocalPort:"
                + LocalPort + ", RemoteAddr:" + RemoteAddr + ", RemoteName:" + RemoteName + ", RemotePort:" + RemotePort
                + ", ServerName:" + ServerName + ", ServerPort:" + ServerPort + "}";
    }

}