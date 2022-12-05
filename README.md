# Report Health Service

- [Report Health Service](#report-health-service)
  - [Service Purpose](#service-purpose)
  - [Service Feature](#service-feature)
  - [Install Service](#install-service)
  - [Start Service](#start-service)
  - [Verify or Monitor Service](#verify-or-monitor-service)
  - [Stop Service](#stop-service)
  - [Q & A](#q--a)

## Service Purpose

Since I forgot to make a health report every morning, I want to provide a health report service that automatically assists users to make a health report on a regular basis.

## Service Feature

1. Automatically report personal health status on working days at 08:30 a.m. each week (default).
2. Use random user agent and referer.

## Install Service

1. Download Repository from Gitlab and checkout the latest branch

   ```bash
   git clone https://github.com/max533/report_health_service.git
   cd report_health_service
   ```

2. Setup environment variable and user information

    2.2 Copy environment template file

    ```bash
    cp .env.template .env
    ```

    2.3 Use `nano` editor (others is OK) open environment file and update variable value

    ```bash
    nano .env
    ```

    2.4 Choose one commute way value in `.env` file.

    ```text
    commute way option
    COMMUTE_WAY=1   => 自行開車、騎車
    COMMUTE_WAY=2   => 搭乘大眾運輸系統
    COMMUTE_WAY=3   => 搭乘公司上下班交通車
    COMMUTE_WAY=4   => 其他
    COMMUTE_WAY=5   => 今日未進辦公室
    ```

    2.5 Below content is `.env` sample file.

    ```text
    # own employee id
    EMPLOYEE_ID=xxxxxxxx
    # commute way
    COMMUTE_WAY=1
    # random time range(recommendation value is 5-20 (second))
    DELAY_TIME_RANGE=10
    TZ=Asia/Taipei  # timezone
    REPORT_PAGE_URL= ### fill company report page url ###
    REPORT_FORM_URL= ### fill company report form url ###
    LOGIN_PAGE_URL= ### fill company login page url ###
    LOGIN_FORM_URL= ### fill company login form url ###
    REFERER_SITE_PATH=referer_site   # No need to modify
    USER_AGENT_PATH=user_agent   # No need to modify
    ```

## Start Service

Build and run Health Report Service. (please check `docker` and `docker-compose` installed in your machine before executing build.)

```bash
sudo docker-compose build
sudo docker-compose up -d
```

## Verify or Monitor Service

Check / monitor the service run correctly.

```bash
$ sudo docker-compose logs

app_1  | Health Report Service start at Fri Jul 30 13:49:09 CST 2021
app_1  |
app_1  | Health Report Date: 2021-07-30
app_1  | 2021-07-30 13:49:22,809 - report_health - line_number : 196 - __main__ - INFO - {'user': 'xxxxxxxx', 'report_status': 'complete but repeatedly', 'report_date': '2021/07/30'}
app_1  | 2021-07-30 13:49:22,811 - report_health - line_number : 239 - __main__ - INFO - This health report program takes 13 s
app_1  |
```

## Stop Service

Stop Service and remove container

```bash
sudo docker-compose down -v
```

## Q & A

1. How to replace repository source in company's internal network?

    - 1.1 Backup original apt source.list

        ```bash
        cp /etc/apt/source.list /etc/apt/source.list.backup
        ```

    - 2.1 Replace official site with NCHC stie

        ```bash
        sudo sed -i 's/archive.ubuntu.com/free.nchc.org.tw/g' /etc/apt/sources.list
        ```

2. How to install `docker` on my machine?

    Answer: <https://docs.docker.com/engine/install/ubuntu/>

3. How to install `docker-compose` if my machine is lack of `docker-compose`.

    Answer : <https://docs.docker.com/compose/install/>

4. How to execute `docker-compose` without `sudo` command.

    Answer : <https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user>
