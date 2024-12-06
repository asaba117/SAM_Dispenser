# **SAM Dispenser**
A project to design a **Semi-Automatic Medication Dispenser (SAM Dispenser)**. This device leverages the **UNB Development Board** to create an efficient, user-friendly system for dispensing medication.

## **Project Overview**
The SAM Dispenser is designed to streamline medication dispensing in healthcare settings. It integrates various sensors and output devices to ensure reliability and accessibility for both patients and caregivers.

### **Features**
- Automated dispensing triggered by sensors and button inputs.
- Real-time feedback using LEDs and a buzzer.
- Controlled operation of a DC motor for dispensing pills.
- Modular design for easy maintenance and upgrades.

---

## **Hardware Components**

### **Inputs**
1. **Button:**  
   Manual input for triggering the dispensing mechanism.
2. **Flight Sensor:**  
   Measures proximity or distance to ensure proper alignment during dispensing.
3. **Pressure Sensor:**  
   Detects the presence or removal of medication to confirm successful dispensing.

### **Outputs**
1. **4 LEDs:**  
   Provide visual feedback for different states:
   - Ready
   - Dispensing
   - Error
   - Complete
2. **Buzzer:**  
   Audible alert for notifications or errors.
3. **DC Motor:**  
   Drives the mechanical dispensing system.

---

## **System Requirements**
- **UNB Development Board:** Central control unit for handling inputs, processing, and driving outputs.
- **Power Supply:** Ensure sufficient voltage and current for the motor, LEDs, sensors, and board.
- **Additional Components:** Resistors, capacitors, pull-up resistors for I²C communication.

---

## **Installation and Usage**

### **1. Wiring**
- Connect all inputs and outputs to the UNB Dev Board as per the schematic.
- Ensure proper grounding and power connections.

### **2. Programming**
- Load the SAM Dispenser firmware onto the UNB Dev Board.
- Calibrate sensors (e.g., Flight and Pressure Sensors) for optimal accuracy.

### **3. Operation**
- Press the button or trigger sensors to start the dispensing process.
- Observe LED and buzzer feedback during operation.

---

## **How It Works**

### **1. Inputs**
- The button initiates manual dispensing.
- The flight sensor ensures medication is loaded, and the pressure sensor verifies medication presence.

### **2. Processing**
- The UNB Dev Board processes the input signals and drives the appropriate outputs.

### **3. Outputs**
- LEDs indicate system status.
- The buzzer alerts users of errors or completion.
- The DC motor dispenses the medication.

---

## **Future Improvements**
- Adding a wireless module for remote operation.
- Integrating a real-time clock for scheduled dispensing.
- Implementing a locking device for medication compartment.
