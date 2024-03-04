
class VotingButtons extends HTMLElement {
  constructor() {
    super();
    this.innerHTML = `
    <button class="button" value="upvote">+</button>
    <div>
      <span class="tag is-large is-white has-text-centered">0</span>
    </div>
    <button class="button" value="downvote">−</button> `
    this.label = this.querySelector('span')
    this.noRefreshVotingNumber = Number(this.label.innerText);

    this.upvoteButton = this.querySelector('button[value="upvote"]');
    this.downvoteButton = this.querySelector('button[value="downvote"]');

    this.upvoteButton.onclick = e => {
      if (this.userVote === '1') {
        this.userVote = '0';
        return;
      }
      this.userVote = '1';
    };

    this.downvoteButton.onclick = e => {
      if (this.userVote === '-1') {
        this.userVote = '0';
        return;
      }
      this.userVote = '-1';
    };
  }

  static get observedAttributes() {
    return ['data-uservote'];
  }
  
  get userVote() {
    return this.getAttribute('data-uservote');
  }

  get upvoteUrl() {
    return this.getAttribute('data-upvote-url');
  }

  get downvoteUrl() {
    return this.getAttribute('data-downvote-url');
  }

  get nullifyUrl() {
    return this.getAttribute('data-nullify-url');
  }

  get messageId() {
    return this.getAttribute('data-message-id');
  }

  set labelText(number) {
    this.label.innerText = number;
  }

  set userVote(vote) {
    if (!(['-1', '0', '1'].includes(vote)))
    {
      throw new Error(`vote ${vote} not valide`);
    }
    this.setAttribute('data-uservote', vote);
  }

  attributeChangedCallback(name, oldValue, newValue) {
    if (oldValue === null) return;
    if (name === 'data-uservote') {
      this.updateStyle(newValue);
    }
  }

  async updateStyle(userVote) {
    if (userVote === '-1') {
      const response = await this.postData(this.downvoteUrl,
        { messageId: this.messageId });
      this.labelText = this.noRefreshVotingNumber - 1;
      this.downvoteButton.classList.add('is-link');
      this.upvoteButton.classList.remove('is-link');
    } else if (userVote === '0') {
      const response = await this.postData(this.nullifyUrl,
        { messageId: this.messageId });
      this.labelText = this.noRefreshVotingNumber;
      this.downvoteButton.classList.remove('is-link');
      this.upvoteButton.classList.remove('is-link');
    } else if (userVote === '1') {
      const response = await this.postData(this.upvoteUrl,
        { messageId: this.messageId });
      this.labelText = this.noRefreshVotingNumber + 1;
      this.downvoteButton.classList.remove('is-link');
      this.upvoteButton.classList.add('is-link');
    }
  }

  async postData(url = "", data = {}) {
    const response = await fetch(url, {
      method: "POST", 
      mode: "cors", 
      cache: "no-cache", 
      credentials: "same-origin", 
      headers: {
        "Content-Type": "application/json",
      },
      redirect: "follow",
      referrerPolicy: "no-referrer",
      body: JSON.stringify(data),
    });
    return response.json();
  }

}
customElements.define('voting-buttons', VotingButtons);


