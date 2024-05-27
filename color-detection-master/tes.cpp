#include <Arduino.h>
#include <Arduino_FreeRTOS.h>
#include <semphr.h>

SemaphoreHandle_t SemaphoreX;

void TaskPIR(void *pvParameters);
void TaskIR(void *pvParameters);
void TaskLED(void *pvParameters);
void TaskAnalogRead(void *pvParameters);

void setup()
{
    Serial.begin(9600);
    while (!Serial)
    {
    ;
    }
    if (SemaphoreX == NULL)
    {
        SemaphoreX = xSemaphoreCreateMutex();
        if ((SemaphoreX) != NULL)
            xSemaphoreGive((SemaphoreX));
    }

    xTaskCreate(
        TaskPIR, "PIR"
        , 128
        , NULL
        , 0
        , NULL
    );

    xTaskCreate(
        TaskIR, "IR"
        , 128
        , NULL
        , 1
        , NULL
    );

    xTaskCreate(
        TaskLED
        , "LED"
        , 128
        , NULL
        , 2
        , NULL
    );

    xTaskCreate(
        TaskAnalogRead
        , "Analog"
        , 128
        , NULL
        , 3
        , NULL
    );
}

void loop(){

}

void TaskPIR(void *pvParameters attribute((unused)))
{
    pinMode(8, INPUT_PULLUP);
    pinMode(9, OUTPUT);
    for (;;)
    {
        if ( xSemaphoreTake( SemaphoreX, ( TickType_t ) 5 ) == pdTRUE ){ 
            int sensorValue = digitalRead(8);
            Serial.print("Kondisi Ruangan : ");
                if (sensorValue == HIGH){
                    Serial.println("Ada Orang !!!");
                    digitalWrite(9, LOW);
                    _delay_ms(500);
                    digitalWrite(9, HIGH);
                    _delay_ms(500);
                    digitalWrite(9, LOW);
                    _delay_ms(500);
                    digitalWrite(9, HIGH);
                    _delay_ms(500);
                }else{
                    Serial.println("Gada Orang");
                    digitalWrite(9, HIGH);
                }
                xSemaphoreGive( SemaphoreX );
        }
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

void TaskIR(void *pvParameters attribute((unused)))
{
    pinMode(6, INPUT);
    for (;;)
    {
        if (xSemaphoreTake(SemaphoreX, (TickType_t)5) ==
            pdTRUE)
        {
            int sensorValue = digitalRead(6);
            Serial.print("Info Halangan : ");
            if (sensorValue == LOW)
            {
                Serial.println("Ada Object didepan !!!");
            }
            else
            {
                Serial.println("Gada Object didepan");
            }
            xSemaphoreGive(SemaphoreX);
        }
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

void TaskLED(void *pvParameters attribute((unused)))
{
    pinMode(13, OUTPUT);
    pinMode(2, INPUT_PULLUP);
    for (;;)
    {
        if (xSemaphoreTake(SemaphoreX, (TickType_t)5) ==
            pdTRUE)
        {
            if (digitalRead(2) == HIGH)
            {
                digitalWrite(13, HIGH);
                Serial.println("Lampu Nyala");
            }
            else
            {
                digitalWrite(13, LOW);
                Serial.println("Lampu Mati");
            }

            xSemaphoreGive(SemaphoreX);
        }
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

void TaskAnalogRead(void *pvParameters attribute((unused)))
{
    for (;;)
    {
        int sensorValue = analogRead(A0);
        if (xSemaphoreTake(SemaphoreX, (TickType_t)5) ==
            pdTRUE)
        {
            Serial.println(sensorValue);
            xSemaphoreGive(SemaphoreX);
        }
        vTaskDelay(pdMS_TO_TICKS(2000));
    }
}
