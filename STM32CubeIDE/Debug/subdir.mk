################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (14.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../lsm6dsl.c \
../stm32l475e_iot01_accelero.c 

OBJS += \
./lsm6dsl.o \
./stm32l475e_iot01_accelero.o 

C_DEPS += \
./lsm6dsl.d \
./stm32l475e_iot01_accelero.d 


# Each subdirectory must supply rules for building sources it contributes
%.o %.su %.cyclo: ../%.c subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DUSE_HAL_DRIVER -DUSE_STM32L475E_IOT01 -DSTM32L475xx -c -I../../Inc -I../../../../../../../Drivers/BSP/Components/lsm6dsl -I../../../../../../../Drivers/BSP/Components/Common -I../../../Common/Inc -I../../../../../../../Drivers/CMSIS/Include -I../../../../../../../Drivers/CMSIS/Device/ST/STM32L4xx/Include -I../../../../../../../Drivers/STM32L4xx_HAL_Driver/Inc -I../../../../../../../Drivers/BSP/B-L475E-IOT01 -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean--2e-

clean--2e-:
	-$(RM) ./lsm6dsl.cyclo ./lsm6dsl.d ./lsm6dsl.o ./lsm6dsl.su ./stm32l475e_iot01_accelero.cyclo ./stm32l475e_iot01_accelero.d ./stm32l475e_iot01_accelero.o ./stm32l475e_iot01_accelero.su

.PHONY: clean--2e-

