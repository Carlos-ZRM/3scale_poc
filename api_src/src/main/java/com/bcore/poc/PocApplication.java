package com.bcore.poc;

import java.text.SimpleDateFormat;
import java.util.Date;

import javax.servlet.http.HttpServletRequest;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.http.HttpHeaders;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
@RequestMapping("/")
public class PocApplication {

	@GetMapping()
	public GetInfo getInfo(HttpServletRequest request, @RequestHeader HttpHeaders headers) {
		GetInfo info = new GetInfo();

		info.setLocalAddr(request.getLocalAddr());
		info.setLocalName(request.getLocalName());
		info.setLocalPort(request.getLocalPort());

		info.setRemoteAddr(request.getRemoteAddr());
		info.setRemotePort(request.getRemotePort());
		info.setRemoteName(request.getRemoteHost());

		info.setServerPort(request.getServerPort());
		info.setServerName(request.getServerName());
		String now = (new SimpleDateFormat("dd/MM/yyyy HH:mm:ss")).format(new Date());
		info.setDate(now);

		System.out.println(info.toString());

		return info;
	}

	public static void main(String[] args) {
		SpringApplication.run(PocApplication.class, args);
	}

}