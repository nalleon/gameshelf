package es.gameshelf.domain.interfaces.service;

import es.gameshelf.domain.Game;
import es.gameshelf.domain.PhotoReview;
import es.gameshelf.domain.Review;
import es.gameshelf.domain.User;

import java.util.List;
import java.util.Set;

/**
 * @author Nabil L. A. @nalleon
 */
public interface IReviewService {
    Review add(String content, User user, Game game, Set<PhotoReview> photoReviewSet);
    List<Review> findAll();
    Review findById(Integer id);
    List<Review> findAllByUser(User user);
    List<Review> findAllByGame(Game game);
    List<Review> findAllByUserLatest(User user);
    List<Review> findAllByGameLatest(Game game);
    boolean delete(Integer id);
    Review update(Integer id, String content, User user, Game game, Set<PhotoReview> photoReviewSet);
}
