# IRC

> **IRC**（Internet Relay Chat的縮寫，「網際網路中繼聊天」）是一種通過網路的即時聊天方式。其主要用於群體聊天，但同樣也可以用於個人對個人的聊天。
> By. Wikipedia

- IRC 的連線需要：
  - Server & Port：建立連線需要
  - Channel：頻道，或是說一個聊天室
  - Nick：昵稱
  - Password：連線密碼

- 協定：

  - 類似 `HTTP` 和 `FTP` 等協定，在  `TCP` 之下以每行 `Command Parameters\r\n` 形式傳遞訊息。

  - 例如：

    ``` 
    PASS secretpasswordhere
    NICK Wiz
    ```

  - 交流：

    - 接收訊息：
      - `/^:([^!]*)!(\S*) PRIVMSG (#\S+) :(.*)$/`
    - 發送訊息：
      - `print $sock "PRIVMSG $chnl :[UDP-Flood Started on $ip for $time seconds]\r\n";` ( `bot.pl.1: 96` )

  - 錯誤訊息：

    - `bot.pl.1: 46` 
      ```
      433    ERR_NICKNAMEINUSE
             "<nick> :Nickname is already in use"
      ```

- See also:
  - > 維基百科:IRC教程 - 維基百科，自由的百科全書
    > https://zh.wikipedia.org/wiki/Wikipedia:IRC%E6%95%99%E7%A8%8B

  - > RFC 2812 - Internet Relay Chat: Client Protocol
    > https://tools.ietf.org/html/rfc2812