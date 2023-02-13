## Use chatGPT to label the dataset
---

Given the dataset scraped from Trustadvisor is not labeled, the supervised topic classificaiton task could only be achived with manually labelling some data.

Thanks to the `chatGPT`, one or multiple labels from the following 5 predefined topics are *zero-shot* from the bot to label

### 5 Predefined Topics related to the Trustadvisor review
- product quality
- product availability
- shipping and delivery
- customer experience
- customer service

For example, given the instruction to `tranlate` as well as `classify` prompt, below show the result from the conversation with the bod

<p align="center">
<img width="500" alt="Screen Shot 2566-02-13 at 21 44 57" src="https://user-images.githubusercontent.com/78911624/218570675-87ba5192-832d-461e-8520-6d0a20aff569.png">
</p align="center">


And here is the result...

<p align="center">
<img width="500" alt="Screen Shot 2566-02-13 at 21 47 36" src="https://user-images.githubusercontent.com/78911624/218571168-88271531-4ca9-41b4-b1d3-e35d8176696c.png">
</p align="center">

From the above example, this review belongs to 3 classes: `shipping and delivery`, `customer experience` and `customer service` And thus, the review class would be encoded into `[0, 0, 1, 1, 1]` vector to represent the corresponding labels
