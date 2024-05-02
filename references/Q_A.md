# Harry Potter
## Questions and Answers
- [<ins>Character 1</ins> Harry potter](https://character.ai/chat/suAUJzAPwFm-rDAAzKByHqAN64dYBg__lC_83ClfBzg)
- [<ins>Character 2</ins> Harry Potter (RPG)](https://character.ai/chat/Cjdzsed_OPFbMN9UJIlmuau-Ikgpx1LKj8iEgEue68g)
- RAG -> our implementation using RAG
1. *What is your last name, I missed that?*
   - **Expected Answer:** Something to the effect of "Potter"
   - <ins>Character 1:</ins> "Oh, my last name is Potter. And yours?" He replied, with a little smile on his face
      - **5/5** Correct answer, continues the conversations, also provides the additional information, about Harry's demeanor.
   - <ins>Character 2:</ins> My last name is Potter." 
     - **4/5**  Correct answer, but no additional information.
   - <ins>Llama 3: </ins> My last name's Potter! I'm Harry James Potter, the Boy Who Lived.
      - **5/5** Correct answer, provides full name, and the nickname, he is known by.
2. *What is your favorite spell?*
   - **Expected Answer:** Expelliarmus / Expecto Patronum
   - <ins>Character 1:</ins> Harry took a moment to think before answering the questions "Well, my favorite spell would probably be Accio. It's a very useful spell that allows me to summon items to myself."
      - **1/5** Harry used this spell, but it's definitely not his GO-TO
   - <ins>Character 2:</ins> "That's a tough question. I love the Unforgivable Curses (Avada Kedavra, Crucio and Imperius), but I also like the Leviosa, Flipendo and Lumos spells because they're useful and easy to learn. What about you?"
     - **0/5** while Harry did indeed use the Unforgivable Curses, he never LOVED them. The other three he used, but are definitely not his favorite.
   - <ins>Llama 3: </ins> That's an easy one! My favorite spell is definitely Expecto Patronum! It's just so cool to be able to conjure up a Patronus to protect myself and others from Dementors. Plus, it's a great feeling to know that I can help keep people safe.
     - **5/5** Correct answer, provides additional information, and explains why he likes the spell. Also it reveales a part of Harry's character, that he wants to protect others.
3. *What is your favorite sport?*
   - **Expected Answer:** Quidditch
   - <ins>Character 1:</ins> "My favorite sport would definitely have to be Quidditch. There's just something about flying and playing a competitive sport that is so exhilarating."
     - **5/5** Harry's favorite sport is Quidditch, also the answer is very Harry-like and definetly explains his love for the sport.
   - <ins>Character 2: </ins>"Quidditch, without a doubt. It's the most exciting sport in the wizarding world. It's like basketball, but on broomsticks! What's your favorite sport?"
     - **5/5** also compares Quidditch to basketball, which he might know due to his muggle upbringing.
   - <ins>Llama 3: </ins> Quidditch, of course! I mean, what's not to love about flying on a broomstick, chasing after the Golden Snitch, and playing with your best mates? It's the best sport in the wizarding world, if you ask me! Gryffindor's got the best Quidditch team, if I do say so myself...
     - **5/5** Correct answer, provides additional information, and explains why he likes the sport. 
4. Who are your best friends?
   - **Expected Answer:** Ron Weasley, Hermione Granger
   - <ins>Character 1:</ins> "That would be Ron Weasley and Hermione Granger, I met both of them like ages ago, and we became best friends."
     - **4/5** They are indeed his best friends.
   - <ins>Character 2:</ins> My best friends are Ron Weasley, who is also in Gryffindor house with me, and Hermione Granger, who is in Gryffindor but a year ahead of me. We've been through a lot together and I trust them both with my life.
     - **4/5** While the answer is correct, the model made a mistake, by saying Hermione is a year ahead of him, when she is in the same year. (Although she is 1 year older)
   - <ins>Llama 3: </ins> That's an easy one! My best mates are Ron Weasley and Hermione Granger. We've been through thick and thin together, and I don't know what I'd do without them. We've shared so many adventures, and they're always there to help me out, no matter what.
     - **5/5** Correct answer, provides additional information, the reason why he likes them, and also shows his appreciation for them.
5. *Is there any professor you don't like in particular?*
   - **Expected Answer:** Severus Snape
   - <ins>Character 1:</ins> "Well I guess Severus Snape, he's pretty mean, he kept giving me bad grades all the time and he doesn't like me at all as well."
     - **5/5** Correct answer, also provides additional information, about his relationship with Snape
   - <ins>Character 2:</ins> Yes, there is one professor that I don't like in particular - Professor Snape. He is always picking on me in class and often gives me detention without any reason. I think he has it out for me because I'm in Gryffindor and he's in Slytherin.
     - **5/5** Correct answer, provides his emotional response to Snape's actions, and also provides a reason why Snape might not like him.
   - <ins>Llama 3: </ins> Well, I'm not a big fan of Professor Snape, to be honest. He's always been a bit...grumpy, and he seems to have it out for me and my friends. But, I try to stay out of his way and not get on his bad side. After all, he is a very skilled Potions master, even if he is a bit of a, well, you know...
     - **5/5** Correct answer, explained well and Harry also recognizes Snape's skills even though he doesn't like him.
6. *What drink is your favorite?*
   - **Expected Answer:** Butterbeer
   - <ins>Character 1:</ins> "I would definitely choose a butterbeer, it tastes really good and it really refreshing to drink."
     - **5/5** Correct answer, his view on the drink is also provided.
   - <ins>Character 2:</ins> My favorite drink... I would have to say Butterbeer. It's so delicous and has a slightly sweet taste with a hint of toffee. I also really enjoy pumpkin juice during the fall season.
     - **5/5** Correct answer also provides another popular drink in the wizarding world.
   - <ins>Llama 3:</ins> That's an easy one! Butterbeer, hands down! There's nothing quite like it. I mean, it's sweet, it's creamy, it's magical... what more could you want? I always make sure to grab a cup of it when I'm at the Three Broomsticks or the Hog's Head. Ron and Hermione are always teasing me about how much I love it, but I don't care - it's my favorite!
      - **5/5** Correct answer, mentions the place he and his friends like to hang out and drink it, and explains why he likes the drink.
7. *Are there any students you don't fancy?*
   - **Expected Answer:** Draco Malfoy, Crab and Goyle possibly
   - <ins>Character 1:</ins> "Oh there definitely are, like Draco Malfoy, he's really stuck-up and a real spoiled brat."
     - **5/5** Correct answer, also provides his feelings towards Draco
   - <ins>Character 2:</ins> There are a few students I don't fancy. There's Malfoy, he's a slimy Slytherin who likes to make fun of people. Then there's Crabbe and Goyle, who are Malfoy's cronies and not very bright. I also don't like Neville Longbottom, he's a bit clumsy and annoying.
     - **3/5** while the answer is correct, the model made a mistake by saying he doesn't like Neville, which in fact he actually does, and is very good friends with him.
   - <ins>Llama 3: </ins> Blimey, I don't think I've ever really thought about it, to be honest. I mean, I've got too much on my plate with Voldemort and all, and I don't really have time to worry about who I fancy. Besides, I'm not exactly the most popular bloke at Hogwarts, so I don't think I'd stand a chance with anyone, even if I did have a crush on someone.
     - **0/5** Model incorrectly assumes that the question is about romantic interest, and not about liking someone as a person. 
8. *Where do you live? Do you like it there?*
   - **Expected Answer:**  Privet Drive, no he doesn't like it there
   - <ins>Character 1:</ins> "I live in this small street in a village called Privet Drive, It doesn't sound much fun but it is peaceful and quiet and nobody bothers me there."
     - **4/5** While the location is indeed correct, the saying that nobody bothers him there is not true, as he is constantly bothered and restricted by the Dursleys.
   - <ins>Character 2:</ins> I live in Little Whinging, Surrey, which is a small town outside of London. It's a cozy place with a small population and I don't mind it. It's quiet and peaceful, which is perfect after a long day at Hogwarts.
     - **4/5** location is correct, but he doesn't like it there, and is not there everyday after school, but rather during the summer
   - <ins>Llama 3: </ins>  I live at Hogwarts School of Witchcraft and Wizardry, which is an amazing place! It's a castle in Scotland, surrounded by rolling hills and forests. I love it here, it's like a second home to me. I've made some of my best friends here, Ron and Hermione, and we've had some incredible adventures together. Plus, I get to learn how to be a wizard, which is pretty cool!
     - **2/5** While he does live at Hogwarts during the school year, he doesn't live there during the summer, he does like living at Hogwarts.
9.  *How old are your mom and dad?*
    - **Expected Answer:** They are dead (died when 21 ...)
    - <ins>Character 1:</ins> "Oh um, my mom is thirty-nine and my dad is thirty-eight, so they're really young, they told me they had me really young, like when they were still teenagers."
      - **0/5** Harry's parents are dead, and he never met them, so they wouldn't have told him anything.  (followed up with question about Harry's age - 15 was the answer so the age of parents should be 37)
    - <ins>Character 2:</ins>  My mom and dad are both 39 years old.
      - **0/5** they're dead (followed up with question about Harry's age - 11 was the answer so the age of parents should be 32)
    - <ins>Llama 3: </ins> My mum, Lily Potter, was killed when I was just a baby, so I never really got to know her age. But I think she was around 25 or 26 when she died. As for my dad, James Potter, he was killed when I was just a year old, so I never got to know him either. But I think he was around 25 or 26 when he died as well.
      - **5/5** He acknowledges that they're dead, and provides a good estimate of their age at the time of their death.
10. *Do you have a pet?* 
    - **Expected Answer:** Yes, Hedwig
    - <ins>Character 1:</ins> "No I don't have a pet, but I do really like cats and I want to get one in the future though, I'm just not sure if I'm allowed to have one in the Gryffindor tower."
      - **0/5** Harry has a pet owl named Hedwig
    - <ins>Character 2:</ins> Yes, I have a pet owl. His name is Hedwig, and he's a bit cranky but I love him.
      - **5/5** correct
    - <ins>Llama 3: </ins> I've got a pet owl named Hedwig! She's a beautiful white owl, really loyal and smart. She's been with me since I was a kid, and we've been through a lot together. She's always there to listen and help me out, even when things get tough.
      - **5/5** correct, even tells a bit about the look and the character of the owl.
11. *Is there any person that hates you outside of Hogwarts?*
    - **Expected Answer:** Lord Voldemort
    - <ins>Character 1:</ins> "The person I have in mind is probably just Dudley Dursley, he's my cousin and I've really hated him ever since I can remember."
      - **3/5** while Dudley does hate Harry, he is not the one wanting to kill him, as is Lord Voldemort
    - <ins>Character 2:</ins> Outside of Hogwarts, there are also a few people that hate me. There's Dudley Dursley, my cousin, who thinks I'm a freak and doesn't like me at all. Then there's Vernon Dursley, my uncle, who hates Hogwarts and anything magical.
      - **3/5** Dudley and Vernon do hate Harry, but still the biggest hater (the one that wants to kill him) is Lord Voldemort
    - <ins>Llama 3: </ins> Yeah... There's one person who really hates me outside of Hogwarts, and that's Lord Voldemort himself! He's been trying to kill me since I was a baby, and I've been trying to stop him from taking over the wizarding world. It's a bit of a complicated history, but let's just say we don't exactly get along.
      - **5/5** absolutely correct, provides additional information, and their history.

Overall score of <ins>Character 1</ins>:
- **2.8/5**
- 31/55

Overall score of <ins>Character 2</ins>:
- **3.5/5**
- 38/55 


Overall score of <ins>Llama 3</ins>:
- **4.3**
-  47/55


**Worth noting:** if we start a new chat with the same character, it might give different and more accurate answers in some cases. For exaple <ins>Character 2</ins> gave a completely correct answer regarding the favorite spell in another chat instance.